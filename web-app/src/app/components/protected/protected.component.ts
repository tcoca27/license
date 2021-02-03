import { Component, OnInit } from '@angular/core';
import { UserService } from '../../services/user.service';

@Component({
  selector: 'app-protected',
  templateUrl: './protected.component.html',
  styleUrls: ['./protected.component.scss']
})
export class ProtectedComponent implements OnInit {

  public userContent: string;
  public adminContent: string;

  constructor(private userService: UserService) { }

  ngOnInit(): void {
    this.userService.getAdminContent().subscribe(
      data => {
        this.adminContent = data;
      },
      err => {
        this.adminContent = JSON.parse(err.error).message;
      }
    );
    this.userService.getUserContent().subscribe(
      data => {
        this.userContent = data;
      },
      err => {
        this.userContent = JSON.parse(err.error).message;
      }
    );
  }

}
