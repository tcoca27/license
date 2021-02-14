package cs.ubbcluj.ro.license.payload.response;

import java.time.LocalDateTime;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class VideoResponse {

	public String filename;
	public LocalDateTime createdDate;
	public long size;

}
