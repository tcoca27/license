package cs.ubbcluj.ro.license.config;

import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "file")
public class VideoStorageProperties {
	private String uploadDir;
	private String resultsDir;

	public String getUploadDir() {
		return uploadDir;
	}

	public void setUploadDir(String uploadDir) {
		this.uploadDir = uploadDir;
	}

	public String getResultsDir() {
		return resultsDir;
	}

	public void setResultsDir(String resultsDir) {
		this.resultsDir = resultsDir;
	}
}
