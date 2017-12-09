import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { ClarityModule } from 'clarity-angular';
import { ChartsModule } from 'ng2-charts';

import { AppComponent } from './app.component';
import { HeaderComponent } from './header/header.component';

// ngrx main imports
import { StoreModule } from '@ngrx/store';

// service imports
import { DatasetService } from './store/services/dataset.service';

// reducer imports
import { reducer as datasetReducer } from './store/reducers/dataset.reducer';

@NgModule({
	declarations: [AppComponent, HeaderComponent],
	imports: [
		BrowserModule,
		ChartsModule,
		ClarityModule.forRoot(),
		StoreModule.forRoot({
			availableDatasets: datasetReducer
		})
	],
	providers: [DatasetService],
	bootstrap: [AppComponent]
})
export class AppModule {}
