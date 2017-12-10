import { Component } from '@angular/core';
import { get_data } from './test';
let values = get_data('age');
let labels = values[0];
let list_v1 = values[1];
let list_v2 = values[2];
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
    { data: list_v1, label: '>50K' },
    {data: list_v2, label: '<=50k' }
  ];

  chartLabels = labels;

  onChartClick(event) {
    console.log(event);
  }
}
