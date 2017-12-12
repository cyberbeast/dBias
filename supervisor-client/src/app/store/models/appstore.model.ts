import { Dataset } from './dataset.model';
import { Supervisor } from './supervisor.model';
import { Task } from './task.model';
import { Report } from './report.model';

export interface AppStore {
  availableDatasets: Dataset[];
  supervisorConfiguration: Supervisor;
  currentTasks: Task[];
  selectedTask: Task;
  selectedReport: Report;
}
