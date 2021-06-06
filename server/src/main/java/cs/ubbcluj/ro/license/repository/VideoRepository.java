package cs.ubbcluj.ro.license.repository;

import cs.ubbcluj.ro.license.model.Video;
import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface VideoRepository extends JpaRepository<Video, Long> {

	Video findByFileName(String filename);

	List<Video> findByUsername(String username);

}
