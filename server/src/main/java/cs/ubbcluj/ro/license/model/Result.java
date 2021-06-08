package cs.ubbcluj.ro.license.model;

import java.nio.file.Path;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.validation.constraints.NotBlank;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@Data
@AllArgsConstructor
@NoArgsConstructor
public class Result {

  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  private Long id;

  @NotBlank
  private String storedPath;

  @NotBlank
  private String videoName;

  public Result(Path location, String videoName) {
    storedPath = location.toString();
    this.videoName = videoName;
  }
}
