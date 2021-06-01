package cs.ubbcluj.ro.license.controller;

import static org.apache.tomcat.util.http.fileupload.FileUploadBase.MULTIPART_FORM_DATA;

import cs.ubbcluj.ro.license.config.VideoStorageProperties;
import cs.ubbcluj.ro.license.model.Video;
import cs.ubbcluj.ro.license.payload.response.VideoResponse;
import cs.ubbcluj.ro.license.service.VideoStorageService;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.FileSystemResource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.CrossOrigin;
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

  @PostMapping(value = "/uploadVideo", consumes = MULTIPART_FORM_DATA)
  @PreAuthorize("hasRole('USER') or hasRole('ADMIN')")
  public VideoResponse uploadVideo(@RequestParam("video") MultipartFile video,
      @RequestParam("attColor") String[] attColor, @RequestParam("defColor") String[] defColor) {
    System.out.println(attColor[0]);
    String filename = videoStorageService.storeVideo(video);
    Video createdVideo = videoStorageService.getVideoByFilename(filename);
    return VideoResponse.builder().id(createdVideo.getId()).filename(filename)
        .createdDate(createdVideo.getCreatedDate()).size(createdVideo.getSize()).build();
  }

  @PostMapping("/uploadVideos")
  @PreAuthorize("hasRole('USER') or hasRole('ADMIN')")
  public List<VideoResponse> uploadMultipleVideos(@RequestParam("videos") MultipartFile[] videos,
      @RequestParam("attColor") String[] attColor, @RequestParam("defColor") String[] defColor) {
    return Arrays.asList(videos).stream().map(video -> uploadVideo(video, attColor, defColor))
        .collect(Collectors.toList());
  }

  @GetMapping("info/{id}")
  @PreAuthorize("hasRole('USER') or hasRole('ADMIN')")
  public VideoResponse getOne(@PathVariable Long id) {
    Video video = videoStorageService.getVideo(id);
    return VideoResponse.builder().id(video.getId()).filename(video.getFileName())
        .createdDate(video.getCreatedDate()).size(video.getSize()).build();
  }

  @GetMapping(value = "/{id}", produces = "video/mp4")
  @PreAuthorize("hasRole('USER') or hasRole('ADMIN')")
  public FileSystemResource stream(@PathVariable Long id)
      throws FileNotFoundException {
    Video video = videoStorageService.getVideo(id);
    String storedPath = video.getStoredPath();
    File videoFile = new File(storedPath);
    return new FileSystemResource(videoFile);
  }

  @GetMapping(value = "")
  @PreAuthorize("hasRole('ADMIN')")
  public List<VideoResponse> getAll() {
    return videoStorageService.getVideos().stream().map(
        video -> new VideoResponse(video.getId(), video.getFileName(), video.getCreatedDate(),
            video.getSize())).collect(Collectors.toList());
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
