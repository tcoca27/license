import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent implements OnInit {

  public form: any = {};
  public isSuccessful = false;
  public isSignUpFailed = false;
  public errorMsg = '';


  constructor(private authService: AuthService) {
  }

  ngOnInit(): void {
  }

  public onSubmit(): void {
    this.authService.register(this.form).subscribe(
      data => {
        this.isSignUpFailed = false;
        this.isSuccessful = true;
      }, error => {
        console.log(error);
        this.errorMsg = error.error;
        this.isSignUpFailed = true;
      }
    );
  }

}
