import { Dataset } from './dataset.model';
import { Supervisor } from './supervisor.model';

export interface AppStore {
	availableDatasets: Dataset[];
	supervisorConfiguration: Supervisor;
}
