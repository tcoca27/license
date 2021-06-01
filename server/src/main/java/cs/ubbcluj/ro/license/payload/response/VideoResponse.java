package cs.ubbcluj.ro.license.payload.response;

import java.time.LocalDateTime;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Builder
@Data
@AllArgsConstructor
@NoArgsConstructor
public class VideoResponse {

	public Long id;
	public String filename;
	public LocalDateTime createdDate;
	public long size;

}
