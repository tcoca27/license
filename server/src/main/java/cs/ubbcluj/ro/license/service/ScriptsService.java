package cs.ubbcluj.ro.license.service;

import cs.ubbcluj.ro.license.model.ColorEnum;
import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.http.HttpResponse.BodyHandlers;
import java.util.ArrayList;
import java.util.List;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

@Service
public class ScriptsService {

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
    if(!splitFrames(name)) {
      throw new RuntimeException("Video could not be split");
    }
    HttpRequest request = HttpRequest.newBuilder(
        URI.create(scriptsApi.concat(String.format("side?name=%s",
            name))))
        .header("accept", "application/json")
        .build();

    HttpResponse<String> response = httpClient.send(request, BodyHandlers.ofString());
    return response.body();
  }

  public String paintSegmentation(String name)
      throws IOException, InterruptedException {
    String side = findSide(name);
    if ((side.contains("right") || side.contains("left"))) {
      HttpRequest request = HttpRequest.newBuilder(
          URI.create(
              scriptsApi.concat(String.format("paint?name=%s&side=%s",
                  name, side.strip().replace("\"", "")))))
          .header("accept", "application/json")
          .build();

      HttpResponse<String> response = httpClient.send(request, BodyHandlers.ofString());

      return response.body().strip();

    }
    throw new RuntimeException("Paint Segmentation ran into errors");
  }

  public String personDetection(String name, ColorEnum attColor, ColorEnum defColor)
      throws IOException, InterruptedException {
    if (splitFrames(name)) {
      HttpRequest request = HttpRequest.newBuilder(
          URI.create(
              scriptsApi
                  .concat(String.format("person-teams-detection?name=%s&attColor=%s&defColor=%s",
                      name, attColor, defColor))))
          .header("accept", "application/json")
          .build();

      HttpResponse<String> response = httpClient.send(request, BodyHandlers.ofString());

      return response.body().strip();

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
