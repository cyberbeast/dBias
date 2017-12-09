import { Component, OnInit } from '@angular/core';
import { DatasetService } from '../store/services/dataset.service';
import { Dataset } from '../store/models/dataset.model';

@Component({
	selector: 'app-client',
	templateUrl: './client.component.html',
	styleUrls: ['./client.component.css']
})
export class ClientComponent implements OnInit {
	datasetList: Dataset[];

	constructor(private _datasetService: DatasetService) {}

	test() {
		this._datasetService.refreshDatasets();
	}

	ngOnInit() {
		this.test();
		this._datasetService.availableDatasets$.subscribe(datasets => {
			this.datasetList = datasets;
		});
	}
}
