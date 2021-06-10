package cs.ubbcluj.ro.license.controller;

import static org.apache.tomcat.util.http.fileupload.FileUploadBase.MULTIPART_FORM_DATA;

import cs.ubbcluj.ro.license.config.VideoStorageProperties;
import cs.ubbcluj.ro.license.model.ColorEnum;
import cs.ubbcluj.ro.license.model.Result;
import cs.ubbcluj.ro.license.model.Video;
import cs.ubbcluj.ro.license.payload.response.ResultsResponse;
import cs.ubbcluj.ro.license.payload.response.VideoResponse;
import cs.ubbcluj.ro.license.service.ScriptsService;
import cs.ubbcluj.ro.license.service.VideoStorageService;
import cs.ubbcluj.ro.license.utils.JwtAccessor;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;
import org.apache.commons.io.FileUtils;
import org.apache.commons.io.IOUtils;
import org.apache.tomcat.util.codec.binary.Base64;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.FileSystemResource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.servlet.mvc.method.annotation.StreamingResponseBody;

@RestController
@RequestMapping("/api/videos")
@CrossOrigin(origins = "*", maxAge = 3600)
public class VideoController {

  @Autowired
  private VideoStorageService videoStorageService;

  @Autowired
  private ScriptsService scriptsService;

  @Autowired
  private JwtAccessor jwtAccessor;

  @PostMapping(value = "/uploadVideo", consumes = MULTIPART_FORM_DATA)
  @PreAuthorize("hasRole('USER') or hasRole('ADMIN')")
  public VideoResponse uploadVideo(@RequestParam("video") MultipartFile video,
      @RequestParam("attColor") ColorEnum attColor, @RequestParam("defColor") ColorEnum defColor) {
    String filename = videoStorageService.storeVideo(video, attColor, defColor);
    Video createdVideo = videoStorageService.getVideoByFilename(filename);
    return VideoResponse.builder().id(createdVideo.getId()).filename(filename)
        .createdDate(createdVideo.getCreatedDate()).size(createdVideo.getSize())
        .username(createdVideo.getUsername()).build();
  }

  @PostMapping("/uploadVideos")
  @PreAuthorize("hasRole('USER') or hasRole('ADMIN')")
  public List<VideoResponse> uploadMultipleVideos(@RequestParam("videos") MultipartFile[] videos,
      @RequestParam("attColor") ColorEnum attColor, @RequestParam("defColor") ColorEnum defColor) {
    return Arrays.asList(videos).stream().map(video -> uploadVideo(video, attColor, defColor))
        .collect(Collectors.toList());
  }

  @GetMapping("/info/{id}")
  @PreAuthorize("hasRole('USER') or hasRole('ADMIN')")
  public VideoResponse getOne(@PathVariable Long id) {
    Video video = videoStorageService.getVideo(id);
    return VideoResponse.builder().id(video.getId()).filename(video.getFileName())
        .createdDate(video.getCreatedDate()).size(video.getSize()).username(video.getUsername())
        .build();
  }

  @GetMapping(value = "/results/{id}")
  @PreAuthorize("hasRole('USER') or hasRole('ADMIN')")
  public List<ResultsResponse> getResults(@PathVariable Long id) {
    String videoName = videoStorageService.getVideo(id).getFileName();
    List<Result> results = videoStorageService.getResultsByVideo(videoName);
    List<ResultsResponse> resultsResponses = new ArrayList<>();
    results.forEach(result -> {
      try {
        File file = new File(result.getStoredPath());
        byte[] encoded = Base64.encodeBase64(FileUtils.readFileToByteArray(file));
        String image = String.format("data:image/jpg;base64,%s", new String(encoded, StandardCharsets.US_ASCII));
        resultsResponses.add(ResultsResponse.builder().image(image).build());
      } catch (IOException e) {
        e.printStackTrace();
      }
    });
    return resultsResponses;
  }

  @GetMapping(value = "/{id}", produces = "video/mp4")
  @PreAuthorize("hasRole('USER') or hasRole('ADMIN')")
  public FileSystemResource stream(@PathVariable Long id) {
    Video video = videoStorageService.getVideo(id);
    String storedPath = video.getStoredPath();
    File videoFile = new File(storedPath);
    return new FileSystemResource(videoFile);
  }

  @DeleteMapping(value = "/{id}", produces = "video/mp4")
  @PreAuthorize("hasRole('ADMIN')")
  public ResponseEntity delete(@PathVariable Long id) {
    videoStorageService.deleteVideo(id);
    return new ResponseEntity(HttpStatus.NO_CONTENT);
  }

  @GetMapping(value = "")
  @PreAuthorize("hasRole('ADMIN')")
  public List<VideoResponse> getAll() {
    return videoStorageService.getVideos().stream().map(
        video -> new VideoResponse(video.getId(), video.getFileName(), video.getCreatedDate(),
            video.getSize(), video.getUsername())).collect(Collectors.toList());
  }

  @GetMapping(value = "/my")
  @PreAuthorize("hasRole('ADMIN') or hasRole('USER')")
  public List<VideoResponse> getAllByUser() {
    return videoStorageService.getVideosFromUser(jwtAccessor.getSub()).stream().map(
        video -> new VideoResponse(video.getId(), video.getFileName(), video.getCreatedDate(),
            video.getSize(), video.getUsername())).collect(Collectors.toList());
  }

  @GetMapping(value = "/{id}/paint", produces = "video/mp4")
  @PreAuthorize("hasRole('ADMIN') or hasRole('USER')")
  public ResponseEntity paintSegmentation(@PathVariable Long id)
      throws IOException, InterruptedException {
    Video video = videoStorageService.getVideo(id);
    scriptsService.paintSegmentation(video.getFileName());
    return new ResponseEntity(HttpStatus.OK);
  }

  @GetMapping(value = "/{id}/persons", produces = "video/mp4")
  @PreAuthorize("hasRole('ADMIN') or hasRole('USER')")
  public ResponseEntity personsDetection(@PathVariable Long id)
      throws IOException, InterruptedException {
    Video video = videoStorageService.getVideo(id);
    scriptsService.personDetection(video.getFileName(), video.getAttColor(), video.getDefColor());
    return new ResponseEntity(HttpStatus.OK);
  }

  @GetMapping(value = "/{id}/side", produces = "video/mp4")
  @PreAuthorize("hasRole('ADMIN') or hasRole('USER')")
  public String findSide(@PathVariable Long id)
      throws IOException, InterruptedException {
    Video video = videoStorageService.getVideo(id);
    return scriptsService.findSide(video.getFileName()).strip();
  }

  private void readAndWrite(final InputStream is, OutputStream os)
      throws IOException {
    byte[] data = new byte[2048];
    int read = 0;
    while ((read = is.read(data)) > 0) {
      os.write(data, 0, read);
    }
    os.flush();
  }


}
