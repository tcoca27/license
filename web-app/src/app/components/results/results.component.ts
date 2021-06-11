import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { UserService } from '../../services/user.service';
import { VideosService } from '../../services/videos.service';
import { DomSanitizer } from '@angular/platform-browser';
import { HttpHeaders } from '@angular/common/http';
import { saveAs } from 'file-saver';
import { NgxSpinnerService } from 'ngx-spinner';

@Component({
  selector: 'app-results',
  templateUrl: './results.component.html',
  styleUrls: ['./results.component.scss']
})
export class ResultsComponent implements OnInit {

  constructor(private userService: UserService, private videosService: VideosService, private domSanitizer: DomSanitizer, private spinner: NgxSpinnerService) {
  }

  public fileInfos: Observable<any>;

  public videoSource;

  public videoDetail = null;

  public results = null;

  public imagePath = null;

  public side = '';

  private static fileNameFromHeaders(headers: HttpHeaders, defaultFileName?: string): string {
    const contentDisposition = headers.get('Content-Disposition');
    if (contentDisposition) {
      const match = contentDisposition.match(/filename="?([^;"]+)"?/);
      if (match && match[1]) {
        return match[1];
      }
    }

    return defaultFileName;
  }

  ngOnInit(): void {
    this.fileInfos = this.videosService.getMyVideos();
    this.spinner.show();
    this.spinner.hide();
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
    this.spinner.show();
    this.videosService.paintSegmentation(id).subscribe(
      (response: any) => {
        const filename = ResultsComponent.fileNameFromHeaders(response.headers, 'paint.zip');
        saveAs(response.body, filename);
        this.spinner.hide();
      }, error => {
        console.log(error);
      }
    );
  }

  public personDetection(id: number): void {
    this.spinner.show();
    this.videosService.personsDetection(id).subscribe(
      (response: any) => {
        const filename = ResultsComponent.fileNameFromHeaders(response.headers, 'teams.zip');
        saveAs(response.body, filename);
        this.spinner.hide();
      }, error => {
        console.log(error);
      }
    );
  }

  public findSide(id: number): void {
    this.videosService.findSide(id).subscribe(
      (response: any) => {
        this.side = response;
      }, error => {
        console.log(error);
      }
    );
  }


}
