package cs.ubbcluj.ro.license.service;

import cs.ubbcluj.ro.license.config.VideoStorageProperties;
import cs.ubbcluj.ro.license.exceptions.FileStorageException;
import cs.ubbcluj.ro.license.model.Video;
import cs.ubbcluj.ro.license.repository.VideoRepository;
import cs.ubbcluj.ro.license.utils.JwtAccessor;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.List;
import java.util.Random;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;
import org.springframework.web.multipart.MultipartFile;

@Service
public class VideoStorageService {

  private final Path storageLocation;

  private final VideoRepository videoRepository;

  private final JwtAccessor jwtAccessor;

  @Autowired
  public VideoStorageService(VideoStorageProperties videoStorageProperties,
      VideoRepository videoRepository, JwtAccessor jwtAccessor) {
    this.storageLocation = Paths.get(videoStorageProperties.getUploadDir()).toAbsolutePath()
        .normalize();
    this.videoRepository = videoRepository;
    this.jwtAccessor = jwtAccessor;
    try {
      Files.createDirectories(this.storageLocation);
    } catch (Exception ex) {
      throw new FileStorageException(
          "Could not create the directory where the uploaded files will be stored.", ex);
    }
  }

  public String storeVideo(MultipartFile file) {
    // Normalize file name
    String fileName = StringUtils.cleanPath(file.getOriginalFilename());
    String name_to_save = generateRandomString(10).concat(".mp4");
    System.out.println(name_to_save);

    try {
      // Copy file to the target location (Replacing existing file with the same name)
      Path targetLocation = storageLocation.resolve(name_to_save);
      Files.copy(file.getInputStream(), targetLocation, StandardCopyOption.REPLACE_EXISTING);

      videoRepository.save(new Video(file.getOriginalFilename(), targetLocation, file.getSize(),
          jwtAccessor.getSub()));
      return fileName;
    } catch (IOException ex) {
      throw new FileStorageException("Could not store file " + fileName + ". Please try again!",
          ex);
    }
  }

  public List<Video> getVideos() {
    return videoRepository.findAll();
  }

  public Video getVideo(Long id) {
    return videoRepository.getOne(id);
  }

  public Video getVideoByFilename(String filename) {
    return videoRepository.findByFileName(filename);
  }

  public List<Video> getVideosFromUser(String username) {
  	return videoRepository.findByUsername(username);
	}

	private static String generateRandomString(int limit) {
    int leftLimit = 48; // numeral '0'
    int rightLimit = 122; // letter 'z'
    Random random = new Random();

    return random.ints(leftLimit, rightLimit + 1)
        .filter(i -> (i <= 57 || i >= 65) && (i <= 90 || i >= 97))
        .limit(limit)
        .collect(StringBuilder::new, StringBuilder::appendCodePoint, StringBuilder::append)
        .toString();
  }

  //TODO
}
