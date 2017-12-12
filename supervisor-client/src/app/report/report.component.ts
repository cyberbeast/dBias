import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';
import { TaskService } from '../store/services/task.service';
import { FilterByPipe } from 'ngx-pipes';

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
      this.currentTask = task;
    });
    this._taskService.selectedReport$.subscribe(report => {
      this.currentReport = report;
      console.log(this.currentReport);
    });
  }
}
