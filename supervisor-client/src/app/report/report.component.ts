import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';
import { TaskService } from '../store/services/task.service';
import { FilterByPipe } from 'ngx-pipes';
import { NgxChartsModule } from '@swimlane/ngx-charts';

@Component({
  selector: 'app-report',
  templateUrl: './report.component.html',
  styleUrls: ['./report.component.css'],
  providers: [FilterByPipe]
})
export class ReportComponent implements OnInit {
  o_id;
  currentReport;
  currentTask;
  analysis = [];
  viz = [];
  sv;

  ds_active = {};
  skewed_active = {};

  constructor(
    private route: ActivatedRoute,
    private location: Location,
    private _taskService: TaskService,
    private filterByPipe: FilterByPipe
  ) {}

  ngOnInit() {
    this.getReport();
  }

  getReport() {
    const id = this.route.snapshot.paramMap.get('id');
    this.o_id = id;
    this._taskService.selectTask(id);
    this._taskService.selectReport(id);
    this._taskService.selectedTask$.subscribe(task => {
      console.log('Getting updated task...');
      console.log(task);
      this.currentTask = task;
    });

    this._taskService.selectedReport$.subscribe(report => {
      this.currentReport = report;
      console.log('report component', this.currentReport);
      this.currentReport.sv_distribution_by_salary.map(
        v => (this.ds_active[v.feature] = v.active)
      );
      console.log('DS: ', this.ds_active);

      this.currentReport.sv_skewed.map(
        v => (this.skewed_active[v.feature] = v.active)
      );
      console.log('SKEWED: ', this.skewed_active);
    });
  }

  public lineChartData: Array<any> = [
    { data: [65, 59, 80, 81, 56, 55, 40], label: 'Series A' },
    { data: [28, 48, 40, 19, 86, 27, 90], label: 'Series B' },
    { data: [18, 48, 77, 9, 100, 27, 40], label: 'Series C' }
  ];
  public lineChartLabels: Array<any> = [
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July'
  ];
  public lineChartOptions: any = {
    responsive: true
  };
  public lineChartColors: Array<any> = [
    {
      // grey
      backgroundColor: 'rgba(148,159,177,0.2)',
      borderColor: 'rgba(148,159,177,1)',
      pointBackgroundColor: 'rgba(148,159,177,1)',
      pointBorderColor: '#fff',
      pointHoverBackgroundColor: '#fff',
      pointHoverBorderColor: 'rgba(148,159,177,0.8)'
    },
    {
      // dark grey
      backgroundColor: 'rgba(77,83,96,0.2)',
      borderColor: 'rgba(77,83,96,1)',
      pointBackgroundColor: 'rgba(77,83,96,1)',
      pointBorderColor: '#fff',
      pointHoverBackgroundColor: '#fff',
      pointHoverBorderColor: 'rgba(77,83,96,1)'
    },
    {
      // grey
      backgroundColor: 'rgba(148,159,177,0.2)',
      borderColor: 'rgba(148,159,177,1)',
      pointBackgroundColor: 'rgba(148,159,177,1)',
      pointBorderColor: '#fff',
      pointHoverBackgroundColor: '#fff',
      pointHoverBorderColor: 'rgba(148,159,177,0.8)'
    }
  ];
  public lineChartLegend: boolean = true;
  public lineChartType: string = 'line';

  public randomize(): void {
    let _lineChartData: Array<any> = new Array(this.lineChartData.length);
    for (let i = 0; i < this.lineChartData.length; i++) {
      _lineChartData[i] = {
        data: new Array(this.lineChartData[i].data.length),
        label: this.lineChartData[i].label
      };
      for (let j = 0; j < this.lineChartData[i].data.length; j++) {
        _lineChartData[i].data[j] = Math.floor(Math.random() * 100 + 1);
      }
    }
    this.lineChartData = _lineChartData;
  }

  // events
  public chartClicked(e: any): void {
    console.log(e);
  }

  public chartHovered(e: any): void {
    console.log(e);
  }

  toggleViz(feature, type) {
    console.log('DS; click -', this.ds_active);
    switch (type) {
      case 'DS': {
        console.log('CUR: ' + feature + ' :: ' + this.ds_active[feature]);
        this.ds_active[feature] =
          this.ds_active[feature] == true ? false : true;
        console.log('AFT: ' + feature + ' :: ' + this.ds_active[feature]);
        break;
      }
      case 'SKEWED': {
        console.log('CUR: ' + feature + ' :: ' + this.skewed_active[feature]);
        this.skewed_active[feature] =
          this.skewed_active[feature] == true ? false : true;
        console.log('AFT: ' + feature + ' :: ' + this.skewed_active[feature]);
        break;
      }
    }
    // this._taskService.toggleViz(feature, type);
  }
}
