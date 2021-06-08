import { Component, OnInit } from '@angular/core';
import { UserService } from '../../services/user.service';
import { VideosService } from '../../services/videos.service';
import { Observable } from 'rxjs';
import { HttpEventType, HttpResponse } from '@angular/common/http';
import DateTimeFormat = Intl.DateTimeFormat;
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import { UserComponent } from '../user/user.component';

@Component({
  selector: 'app-protected',
  templateUrl: './protected.component.html',
  styleUrls: ['./protected.component.scss']
})
export class ProtectedComponent implements OnInit {

  public userContent: string;
  public adminContent: string;

  public selectedFiles: FileList;
  public progressInfos = [];
  public message = '';
  public videoDetail = null;
  public attColor: string;
  public defColor: string;

  public fileInfos: Observable<any>;

  public videoSource;

  constructor(private userService: UserService, private videosService: VideosService, private domSanitizer: DomSanitizer) {
  }

  ngOnInit(): void {
    this.fileInfos = this.videosService.getVideos();
  }


  public showVideo(id: number): void {
    this.videosService.getVideo(id).subscribe(
      (response: any) => {
        this.videoDetail = response;
      }
    );
    this.videosService.streamVideo(id).subscribe(
      (resp) => {
        console.log(resp);
        this.videoSource = resp;
      }, error => {
        console.log(error);
        console.log('error streaming video');
      }
    );
  }

  public deleteVideo(id: any): void {
    this.videosService.deleteVideo(id).subscribe(() => window.location.reload());
  }

  public deleteUser(): void {
    this.videosService.deleteUser(this.videoDetail.username).subscribe(() => window.location.reload());
  }

  public isCurrentUser(username: string): boolean {
    return this.videosService.isCurrentUser(username);
  }
}
