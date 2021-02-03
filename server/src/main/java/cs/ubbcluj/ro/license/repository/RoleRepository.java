package cs.ubbcluj.ro.license.repository;

import cs.ubbcluj.ro.license.model.Role;
import cs.ubbcluj.ro.license.model.RoleEnum;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface RoleRepository extends JpaRepository<Role, Long> {
    Optional<Role> findByName(RoleEnum name);
}
