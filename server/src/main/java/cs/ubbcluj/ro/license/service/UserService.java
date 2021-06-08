package cs.ubbcluj.ro.license.service;

import cs.ubbcluj.ro.license.model.User;
import cs.ubbcluj.ro.license.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class UserService {

  @Autowired
  private UserRepository userRepository;

  @Autowired
  private VideoStorageService videoStorageService;

  @Transactional
  public User deleteUser(String username) {
    User user = userRepository.findByUsername(username).orElseThrow(() -> new RuntimeException("No user found with this username."));
    userRepository.delete(user);
    videoStorageService.deleteVideosByUser(username);
    return user;
  }

}
