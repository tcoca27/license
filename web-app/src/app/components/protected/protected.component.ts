import { Component, OnInit } from '@angular/core';
import { UserService } from '../../services/user.service';
import { VideosService } from '../../services/videos.service';

@Component({
  selector: 'app-protected',
  templateUrl: './protected.component.html',
  styleUrls: ['./protected.component.scss']
})
export class ProtectedComponent implements OnInit {

  public userContent: string;
  public adminContent: string;

  public loading = false;

  public video: File = null;

  public videos: File[] = [null];

  constructor(private userService: UserService, private videosService: VideosService) { }

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

  public onChange(event, index: number): void {
    console.log(index);
    console.log(event);
    this.video = event.target.files[0];
    this.videos[index] = this.video;
    console.log(this.videos);
  }

  onUpload(): void {
    if (!this.videos[0]) {
      return;
    }
    this.loading = true;
    this.videosService.uploadVideo(this.videos[0]).subscribe(
      (event: any) => {
        if (typeof (event) === 'object') {
          this.loading = false;
        }
      }
    );
  }

  onAddAnother(): void {
    this.videos.push(null);
  }

}
