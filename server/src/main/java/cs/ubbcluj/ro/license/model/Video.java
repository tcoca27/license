package cs.ubbcluj.ro.license.model;

import java.nio.file.Path;
import java.time.LocalDateTime;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.data.annotation.CreatedBy;
import org.springframework.data.annotation.CreatedDate;

@Entity
@Data
@AllArgsConstructor
@NoArgsConstructor
public class Video {

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long id;

	@NotBlank
	private String fileName;

	@NotBlank
	private String storedPath;

	@NotNull
	private long size;

	@CreatedDate
	private LocalDateTime createdDate;

	public Video(String originalFilename, Path targetLocation, long size) {
		fileName = originalFilename;
		storedPath = targetLocation.toString();
		this.size = size;
	}
}
