package cs.ubbcluj.ro.license.controller;

import cs.ubbcluj.ro.license.model.User;
import cs.ubbcluj.ro.license.service.UserService;
import cs.ubbcluj.ro.license.service.VideoStorageService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@CrossOrigin(origins = "*", maxAge = 3600)
@RestController
@RequestMapping("/api/user")
public class UserController {

    @Autowired
    private UserService userService;

    @DeleteMapping("/{username}")
    public ResponseEntity deleteUser(@PathVariable String username) {
        System.out.println(username);
        userService.deleteUser(username);
        return new ResponseEntity(HttpStatus.NO_CONTENT);
    }

}
