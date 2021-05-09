import { AfterViewInit, Component, ElementRef, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { UserService } from '../../services/user.service';
import { Surface } from '@progress/kendo-drawing';
import { drawCourt } from '../../basketball/draw/court-draw';
import { PointXY } from '../../basketball/draw/pointXY';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements AfterViewInit, OnInit, OnDestroy {

  public content: string;

  @ViewChild('surface')
  private surfaceElement: ElementRef;
  private surface: Surface;

  constructor(private userService: UserService) {
  }

  ngOnInit(): void {
    this.userService.getPublicContent().subscribe(
      data => {
        this.content = data;
      }, error => {
        this.content = JSON.parse(error.error).message;
      }
    );
  }

  public ngAfterViewInit(): void {
    drawCourt(this.createSurface(), this.randomlyGenTeam(), this.randomlyGenTeam(), this.randomlyGenPoint());
  }

  public ngOnDestroy(): void {
    this.surface.destroy();
  }

  private createSurface(): Surface {
    // Obtain a reference to the native DOM element of the wrapper
    const element = this.surfaceElement.nativeElement;

    // Create a drawing surface
    this.surface = Surface.create(element);

    return this.surface;
  }

  private randomlyGenTeam(): PointXY[] {
    const result = [];
    for (let i = 0; i < 5; i++) {
      const point = this.randomlyGenPoint();
      result.push(new PointXY(point.x, point.y));
    }
    return result;
  }

  private randomlyGenPoint(): PointXY {
    return new PointXY(Math.floor(Math.random() * 281), Math.floor(Math.random() * 151));
  }

}
