import { Component, OnInit } from '@angular/core';
import { UserService } from '../../services/user.service';
import { VideosService } from '../../services/videos.service';

@Component({
  selector: 'app-user',
  templateUrl: './user.component.html',
  styleUrls: ['./user.component.scss']
})
export class UserComponent implements OnInit {

  public userContent: string;

  public loading = false;

  public video: File = null;

  public videos: File[] = [null];

  constructor(private userService: UserService, private videosService: VideosService) {
  }

  ngOnInit(): void {
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
