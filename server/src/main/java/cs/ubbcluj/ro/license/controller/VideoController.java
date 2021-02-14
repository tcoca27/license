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
	public VideoResponse uploadVideo(@RequestParam("video") MultipartFile video) {
		String filename = videoStorageService.storeVideo(video);
		Video createdVideo = videoStorageService.getVideoByFilename(filename);

		return new VideoResponse(filename, createdVideo.getCreatedDate(), createdVideo.getSize());
	}

	@PostMapping("/uploadVideos")
	@PreAuthorize("hasRole('USER') or hasRole('ADMIN')")
	public List<VideoResponse> uploadMultipleVideos(@RequestParam("videos")MultipartFile[] videos) {
		return Arrays.asList(videos).stream().map(video -> uploadVideo(video)).collect(Collectors.toList());
	}

	@GetMapping("info/{id}")
	@PreAuthorize("hasRole('USER') or hasRole('ADMIN')")
	public VideoResponse getOne(@PathVariable Long id) {
		Video video = videoStorageService.getVideo(id);
		return new VideoResponse(video.getFileName(), video.getCreatedDate(), video.getSize());
	}

	@GetMapping(value = "/{id}")
	@PreAuthorize("hasRole('USER') or hasRole('ADMIN')")
	public StreamingResponseBody stream(@PathVariable Long id)
			throws FileNotFoundException {
		String storedPath = videoStorageService.getVideo(id).getStoredPath();
		File videoFile = new File(storedPath);
		final InputStream videoFileStream = new FileInputStream(videoFile);
		return (os) -> {
			readAndWrite(videoFileStream, os);
		};
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
