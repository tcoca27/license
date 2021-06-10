import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { UserService } from '../../services/user.service';
import { VideosService } from '../../services/videos.service';
import { DomSanitizer } from '@angular/platform-browser';

@Component({
  selector: 'app-results',
  templateUrl: './results.component.html',
  styleUrls: ['./results.component.scss']
})
export class ResultsComponent implements OnInit {

  public fileInfos: Observable<any>;

  public videoSource;

  public videoDetail = null;

  public results = null;

  public imagePath = null;

  constructor(private userService: UserService, private videosService: VideosService, private domSanitizer: DomSanitizer) {
  }

  ngOnInit(): void {
    this.fileInfos = this.videosService.getMyVideos();
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
    this.videosService.getResults(id).subscribe(
      (resp) => {
        console.log(resp);
        this.imagePath = [];
        resp.forEach(r => this.imagePath.push(this.domSanitizer.bypassSecurityTrustResourceUrl(r.image)));
        console.log(this.imagePath);
        this.results = resp;
      }, error => {
        console.log(error);
      }
    );
  }

  public paintSegmentation(id: number): void {
    this.videosService.paintSegmentation(id).subscribe(
      (response: any) => {
        console.log(response);
      }, error => {
        console.log(error);
      }
    );
  }

  public personDetection(id: number): void {
    this.videosService.personsDetection(id).subscribe(
      (response: any) => {
        console.log(response);
      }, error => {
        console.log(error);
      }
    );
  }

  public findSide(id: number): void {
    this.videosService.findSide(id).subscribe(
      (response: any) => {
        console.log(response);
      }, error => {
        console.log(error);
      }
    );
  }
}
