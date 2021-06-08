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
    System.out.println(scriptsApi.concat(String.format("analysis?name=%s&time=%s&attColor=%s&defColor=%s",
        name, 0.1, attColor.toString().toLowerCase(), defColor.toString().toLowerCase())));
    HttpRequest request = HttpRequest.newBuilder(
        URI.create(scriptsApi.concat(String.format("analysis?name=%s&time=%s&attColor=%s&defColor=%s",
            name, 0.1, attColor, defColor))))
        .header("accept", "application/json")
        .build();

    HttpResponse<String> response = httpClient.send(request, BodyHandlers.ofString());

    return tokenize(response.body());
  }

  private List<String> tokenize(String body) {
    System.out.println(body);
    String[] tokens = body.strip().split(",");
    List<String> result = new ArrayList<>();
    for(String token: tokens) {
      token = token.replace("[","");
      token = token.replace("]","");
      result.add(token);
    }
    System.out.println(result);
    return result;
  }
}
