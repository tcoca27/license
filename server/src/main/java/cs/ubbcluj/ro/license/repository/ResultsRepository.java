package cs.ubbcluj.ro.license.repository;

import cs.ubbcluj.ro.license.model.Result;
import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ResultsRepository extends JpaRepository<Result, Long> {
  List<Result> getByVideoName(String videoName);

  Long deleteAllByVideoName(String videoName);
}
