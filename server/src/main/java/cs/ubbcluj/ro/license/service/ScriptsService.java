package cs.ubbcluj.ro.license.service;

import cs.ubbcluj.ro.license.model.ColorEnum;
import cs.ubbcluj.ro.license.model.Result;
import cs.ubbcluj.ro.license.repository.ResultsRepository;
import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.http.HttpResponse.BodyHandlers;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

@Service
public class ScriptsService {

  @Autowired
  private ResultsRepository resultsRepository;

  private final HttpClient httpClient = HttpClient.newHttpClient();

  @Value("${scripts.api}")
  private String scriptsApi;

  public List<String> analysis(String name, ColorEnum attColor, ColorEnum defColor)
      throws IOException, InterruptedException {
    HttpRequest request = HttpRequest.newBuilder(
        URI.create(
            scriptsApi.concat(String.format("analysis?name=%s&time=%s&attColor=%s&defColor=%s",
                name, 0.1, attColor, defColor))))
        .header("accept", "application/json")
        .build();

    HttpResponse<String> response = httpClient.send(request, BodyHandlers.ofString());

    return tokenize(response.body());
  }

  public boolean splitFrames(String name) throws IOException, InterruptedException {
    HttpRequest request = HttpRequest.newBuilder(
        URI.create(scriptsApi.concat(String.format("frames?name=%s&time=%s",
            name, 1))))
        .header("accept", "application/json")
        .build();

    HttpResponse<String> response = httpClient.send(request, BodyHandlers.ofString());
    return (response.body().contains("OK"));
  }

  public String findSide(String name) throws IOException, InterruptedException {
    Optional<Result> result = resultsRepository.findByVideoNameAndStoredPathIsNull(name);
    if (result.isPresent() && result.get().getSide() != null) {
      return result.get().getSide();
    }
    if(!splitFrames(name)) {
      throw new RuntimeException("Video could not be split");
    }
    HttpRequest request = HttpRequest.newBuilder(
        URI.create(scriptsApi.concat(String.format("side?name=%s",
            name))))
        .header("accept", "application/json")
        .build();

    HttpResponse<String> response = httpClient.send(request, BodyHandlers.ofString());
    String side = response.body().strip();
    result.ifPresent(value -> value.setSide(side));
    resultsRepository.save(result.orElse(Result.builder().videoName(name).side(side).build()));
    return side;
  }

  public String paintSegmentation(String name)
      throws IOException, InterruptedException {
    Optional<Result> result = resultsRepository.findByVideoNameAndStoredPathIsNull(name);
    if (result.isPresent() && result.get().getPaintPath() != null) {
      return result.get().getPaintPath();
    }
    String side = findSide(name);
    result = resultsRepository.findByVideoNameAndStoredPathIsNull(name);
    if ((side.contains("right") || side.contains("left"))) {
      HttpRequest request = HttpRequest.newBuilder(
          URI.create(
              scriptsApi.concat(String.format("paint?name=%s&side=%s",
                  name, side.strip().replace("\"", "")))))
          .header("accept", "application/json")
          .build();

      HttpResponse<String> response = httpClient.send(request, BodyHandlers.ofString());

      String path = response.body().strip();
      result.ifPresent(value -> value.setPaintPath(path));
      resultsRepository.save(result.orElse(Result.builder().videoName(name).paintPath(path).build()));
      return path;

    }
    throw new RuntimeException("Paint Segmentation ran into errors");
  }

  public String personDetection(String name, ColorEnum attColor, ColorEnum defColor)
      throws IOException, InterruptedException {
    Optional<Result> result = resultsRepository.findByVideoNameAndStoredPathIsNull(name);
    if (result.isPresent() && result.get().getPersonsPath() != null) {
      return result.get().getPersonsPath();
    }
    if (splitFrames(name)) {
      HttpRequest request = HttpRequest.newBuilder(
          URI.create(
              scriptsApi
                  .concat(String.format("person-teams-detection?name=%s&attColor=%s&defColor=%s",
                      name, attColor, defColor))))
          .header("accept", "application/json")
          .build();

      HttpResponse<String> response = httpClient.send(request, BodyHandlers.ofString());

      String path = response.body().strip();
      result.ifPresent(value -> value.setPersonsPath(path));
      resultsRepository.save(result.orElse(Result.builder().videoName(name).personsPath(path).build()));
      return path;

    }
    throw new RuntimeException("Person Detection ran into errors");
  }

  private List<String> tokenize(String body) {
    System.out.println(body);
    String[] tokens = body.strip().split(",");
    List<String> result = new ArrayList<>();
    for (String token : tokens) {
      token = token.replace("[", "");
      token = token.replace("]", "");
      result.add(token);
    }
    System.out.println(result);
    return result;
  }
}
