import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent {
  title = 'app';
  chartOptions = {
    responsive: true
  };
chartType = 'bar';
  chartData = [
    { data: [39, 50, 53, 38], label: 'Female' },
    {data: [39, 50, 53, 38], label: 'Male' }
  ];

  chartLabels = ['23','24','25','26'];

  onChartClick(event) {
    console.log(event);
  }
}
