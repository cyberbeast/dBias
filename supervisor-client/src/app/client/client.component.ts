import { Component, OnInit, ViewChild } from '@angular/core';
import { DatasetService } from '../store/services/dataset.service';
import { TaskService } from '../store/services/task.service';
import { Dataset } from '../store/models/dataset.model';
import { Task } from '../store/models/task.model';
import { Wizard } from 'clarity-angular';
import { FilterByPipe, PickPipe } from 'ngx-pipes';

@Component({
  selector: 'app-client',
  templateUrl: './client.component.html',
  styleUrls: ['./client.component.css'],
  providers: [FilterByPipe, PickPipe]
})
export class ClientComponent implements OnInit {
  @ViewChild('wizardlg') wizardLarge: Wizard;
  lgOpen: boolean = false;
  datasetList: Dataset[];
  taskList: Task[];
  statusMessage: any;

  constructor(
    private _datasetService: DatasetService,
    private _taskService: TaskService
  ) {}

  openWizard() {
    this.wizardLarge.open();
  }

  test() {
    this._datasetService.refreshDatasets();
  }

  onCommit() {
    this._taskService.newTaskRequest(this.newTaskTemplate);
  }

  doFinish() {
    this.wizardLarge.reset();
    this.newTaskTemplate = {
      name: '',
      description: '',
      dataset: '',
      type: '',
      supervisor: true
    };
  }

  callTrain(id) {
    console.log('ID: ', id);
    this._taskService.trainTaskByID(id);
  }

  ngOnInit() {
    this.test();
    this._datasetService.availableDatasets$.subscribe(datasets => {
      this.datasetList = datasets;
    });

    this._taskService.getSystemTasks();
    this._taskService.currentTasks$.subscribe(tasks => {
      this.taskList = tasks;
    });

    this._taskService.statusStream$.subscribe({
      next: v => (this.statusMessage = v)
    });
  }

  newTaskTemplate = {
    name: '',
    description: '',
    dataset: '',
    type: '',
    supervisor: true
  };
}
