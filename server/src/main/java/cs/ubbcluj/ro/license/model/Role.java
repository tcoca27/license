package cs.ubbcluj.ro.license.model;

import com.fasterxml.jackson.annotation.JsonBackReference;
import lombok.*;

import javax.persistence.*;
import java.util.HashSet;
import java.util.Set;

@Entity
@Getter
@Setter
@EqualsAndHashCode(of = "id")
@Data
@ToString(exclude = {"usersForRole"})
public class Role {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Enumerated(EnumType.STRING)
    @Column(length = 20)
    private RoleEnum name;

    @JsonBackReference
    @ManyToMany(mappedBy = "roles", fetch = FetchType.LAZY)
    private Set<User> usersForRole = new HashSet<>();
}
