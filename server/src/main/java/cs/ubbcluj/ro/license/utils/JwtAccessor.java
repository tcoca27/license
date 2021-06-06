package cs.ubbcluj.ro.license.utils;

import cs.ubbcluj.ro.license.security.services.UserDetailsImpl;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;

@Component
public class JwtAccessor {

  public UserDetailsImpl getAuthenticationPrincipal() {
    return (UserDetailsImpl) SecurityContextHolder.getContext().getAuthentication().getPrincipal();
  }

  public String getSub() {
    return getAuthenticationPrincipal().getUsername();
  }

}
