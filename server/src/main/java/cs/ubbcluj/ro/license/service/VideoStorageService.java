package cs.ubbcluj.ro.license.service;

import cs.ubbcluj.ro.license.config.VideoStorageProperties;
import cs.ubbcluj.ro.license.exceptions.FileStorageException;
import cs.ubbcluj.ro.license.model.ColorEnum;
import cs.ubbcluj.ro.license.model.Result;
import cs.ubbcluj.ro.license.model.Video;
import cs.ubbcluj.ro.license.repository.ResultsRepository;
import cs.ubbcluj.ro.license.repository.VideoRepository;
import cs.ubbcluj.ro.license.utils.JwtAccessor;
import java.io.File;
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

  private final Path resultsLocation;

  private final VideoRepository videoRepository;

  private final ResultsRepository resultsRepository;

  private final JwtAccessor jwtAccessor;

  private final ScriptsService scriptsService;

  @Autowired
  public VideoStorageService(VideoStorageProperties videoStorageProperties,
      VideoRepository videoRepository, JwtAccessor jwtAccessor, ScriptsService scriptsService,
      ResultsRepository resultsRepository) {
    this.storageLocation = Paths.get(videoStorageProperties.getUploadDir()).toAbsolutePath()
        .normalize();
    this.resultsLocation = Paths.get(videoStorageProperties.getResultsDir()).toAbsolutePath()
        .normalize();
    this.videoRepository = videoRepository;
    this.jwtAccessor = jwtAccessor;
    this.scriptsService = scriptsService;
    this.resultsRepository = resultsRepository;
    try {
      Files.createDirectories(this.storageLocation);
    } catch (Exception ex) {
      throw new FileStorageException(
          "Could not create the directory where the uploaded files will be stored.", ex);
    }
  }

  public String storeVideo(MultipartFile file, ColorEnum attColor, ColorEnum defColor) {
    // Normalize file name
    String nameToSave = generateRandomString(10);

    try {
      // Copy file to the target location (Replacing existing file with the same name)
      Path targetLocation = storageLocation.resolve(nameToSave.concat(".mp4"));
      Files.copy(file.getInputStream(), targetLocation, StandardCopyOption.REPLACE_EXISTING);

      videoRepository.save(new Video(nameToSave, targetLocation, file.getSize(),
          jwtAccessor.getSub()));
      new Thread(() -> {
        try {
          analyzeVideo(nameToSave, attColor, defColor);
        } catch (IOException | InterruptedException exception) {
          exception.printStackTrace();
          System.out.println(exception);
        }
      }).start();
//      analyzeVideo(nameToSave, attColor, defColor, fileName);
      return nameToSave;
    } catch (IOException ex) {
      throw new FileStorageException("Could not store file " + nameToSave + ". Please try again!",
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

  public void analyzeVideo(String name, ColorEnum attColor, ColorEnum defColor)
      throws IOException, InterruptedException {
    List<String> results = scriptsService.analysis(name, attColor, defColor);
    results.forEach(result -> {
      String pathToResolve = name.concat("/" + result.strip().replaceAll("\"", ""));
      System.out.println(pathToResolve);
      Path location = resultsLocation.resolve(pathToResolve);
      resultsRepository.save(new Result(location, name));
    });
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

  public List<Result> getResultsByVideo(String videoName) {
    return resultsRepository.getByVideoName(videoName);
  }

  public Video deleteVideo(Long id) {
    Video video = getVideo(id);
    videoRepository.delete(video);
    File file = new File(video.getStoredPath());
    file.delete();
    if (resultsRepository.getByVideoName(video.getFileName()).size() > 0) {
      resultsRepository.deleteAllByVideoName(video.getFileName());
    }
    return video;
  }

  public void deleteVideosByUser(String username) {
    if (videoRepository.findByUsername(username).size() > 0) {
      videoRepository.deleteAllByUsername(username);
    }
  }

  //TODO
}
