import { Surface, Group, FillOptions, Rect, geometry, Path, Circle } from '@progress/kendo-drawing';
const { Rect: RectGeometry, Circle: GeomCircle, Point, Size, transform } = geometry;
import {PointXY} from './pointXY';

// tslint:disable-next-line:typedef
export function drawCourt(surface: Surface, homePlayers: PointXY[], awayPlayers: PointXY[], ballXY: PointXY) {

  // This rectangle demonstrates how to use the gradient as a fill.
  const rect = new RectGeometry(
    new Point(0, 0),
    new Size(getSize(280), getSize(150))
  );

  const drawingRect = new Rect(rect, {
    stroke: {
      color: 'black',
      width: 2
    },
    fill: {
      color: '#dfbb85'
    }
  });

  const boardH = drawLine(getSize(10), getSize(66), getSize(10), getSize(84));
  const boardA = drawLine(getSize(270), getSize(66), getSize(270), getSize(84));
  const tCHU = drawLine(getSize(0), getSize(10), getSize(40), getSize(10));
  const tCHD = drawLine(getSize(0), getSize(140), getSize(40), getSize(140));
  const tCAU = drawLine(getSize(240), getSize(10), getSize(280), getSize(10));
  const tCAD = drawLine(getSize(240), getSize(140), getSize(280), getSize(140));
  const paintAD = drawLine(getSize(234), getSize(94), getSize(280), getSize(94));
  const paintHD = drawLine(getSize(0), getSize(94), getSize(46), getSize(94));
  const paintAU = drawLine(getSize(234), getSize(58), getSize(280), getSize(58));
  const paintHU = drawLine(getSize(0), getSize(58), getSize(46), getSize(58));
  const ftH = drawLine(getSize(46), getSize(58), getSize(46), getSize(94));
  const ftA = drawLine(getSize(234), getSize(58), getSize(234), getSize(94));
  const halfCourt = drawLine(getSize(140), getSize(0), getSize(140), getSize(150));

  const rimH = drawCircle(getSize(15), getSize(75), getSize(3));
  const rimA = drawCircle(getSize(265), getSize(75), getSize(3));
  const halfCourtCircle = drawCircle(getSize(140), getSize(75), getSize(18));
  const paintTopH = drawCircle(getSize(46), getSize(76), getSize(18));
  const paintTopA = drawCircle(getSize(234), getSize(76), getSize(18));

  const threePointH = drawCircle(getSize(15), getSize(75), getSize(70));
  const threePointA = drawCircle(getSize(265), getSize(75), getSize(70));

  const ball = drawPlayer(getSize(ballXY.x), getSize(ballXY.y), getSize(3), 'orange');

  clipPaths(paintTopH, paintTopA, threePointA, threePointH);
  // Place all the shapes in a group.
  const group = new Group();
  group.append(drawingRect, boardH, boardA, tCHU, tCAU, tCHD, tCAD, paintAD, paintAU, paintHU, paintHD,
    ftH, ftA, halfCourt, rimH, rimA, paintTopH, paintTopA, threePointH, threePointA, ball, halfCourtCircle);
  homePlayers.forEach(player => group.append(drawPlayer(getSize(player.x), getSize(player.y), getSize(5), 'green')));
  awayPlayers.forEach(player => group.append(drawPlayer(getSize(player.x), getSize(player.y), getSize(5), 'red')));


  // Render the group on the surface.
  surface.draw(group);
}

function drawLine(startX, startY, endX, endY): Path {
  const path = new Path({
    stroke: {
      color: `black`,
      width: 2
    }
  });
  return path.moveTo(startX, startY).lineTo(endX, endY).close();
}

function getSize(size): number {
  const multiplier = 2;
  return size * multiplier;
}

function drawCircle(centerX, centerY, radius): Circle {
  const circ = new GeomCircle([centerX, centerY], radius);
  return new Circle(circ, {
    stroke: { color: 'black', width: 2 }
  });
}

function drawPlayer(centerX, centerY, radius, color): Circle {
  const circ = new GeomCircle([centerX, centerY], radius);
  return new Circle(circ, {
    stroke: { color, width: 2 },
    fill: { color }
  });
}

function clipPaths(paintTopH, paintTopA, threePointA, threePointH): void {
  const clipPathPH = new Path();
  clipPathPH.moveTo(getSize(46), 0).lineTo(getSize(46), getSize(150))
    .lineTo(getSize(100), getSize(150)).lineTo(getSize(100), 0).close();
  paintTopH.clip(clipPathPH);

  const clipPathPA = new Path();
  clipPathPA.moveTo(getSize(234), 0).lineTo(getSize(234), getSize(150))
    .lineTo(0, 0).close();
  paintTopA.clip(clipPathPA);

  const clipPath3A = new Path();
  clipPath3A.moveTo(getSize(100), 0).lineTo(getSize(100), getSize(150))
    .lineTo(getSize(240), getSize(150)).lineTo(getSize(240), 0).close();
  threePointA.clip(clipPath3A);

  const clipPath3H = new Path();
  clipPath3H.moveTo(getSize(40), 0).lineTo(getSize(40), getSize(150))
    .lineTo(getSize(250), 150).lineTo(getSize(250), 0).close();
  threePointH.clip(clipPath3H);
}
