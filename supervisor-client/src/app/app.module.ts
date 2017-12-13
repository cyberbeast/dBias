import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FormsModule } from '@angular/forms';
import { ClarityModule } from 'clarity-angular';
import { ChartsModule } from 'ng2-charts/ng2-charts';

import { AppComponent } from './app.component';
// import { BarChartDemoComponent } from './app.component';
// import {SkewComponent} from './app.component';
import { HeaderComponent } from './header/header.component';
import { ClientComponent } from './client/client.component';
import { SupervisorComponent } from './supervisor/supervisor.component';
import { ReportComponent } from './report/report.component';
import { TestComponent } from './test/test.component';

import { AceEditorModule } from 'ng2-ace-editor';

// ngrx main imports
import { StoreModule } from '@ngrx/store';

// service imports
import { DatasetService } from './store/services/dataset.service';
import { SupervisorService } from './store/services/supervisor.service';
import { TaskService } from './store/services/task.service';
import { TestService } from './store/services/test.service';

// reducer imports
import { reducer as datasetReducer } from './store/reducers/dataset.reducer';
import { reducer as supervisorReducer } from './store/reducers/supervisor.reducer';
import { reducer as taskReducer } from './store/reducers/task.reducer';
import { reducer as reportReducer } from './store/reducers/report.reducer';
import { reducer as selectTaskReducer } from './store/reducers/selectTask.reducer';
import { reducer as queryTaskReducer } from './store/reducers/queryResult.reducer';

import { IdFilterPipe } from './id-filter.pipe';
import { NgPipesModule } from 'ngx-pipes';

const appRoutes: Routes = [
  { path: 'client', component: ClientComponent },
  { path: 'supervisor', component: SupervisorComponent },
  { path: 'report/:id', component: ReportComponent },
  { path: 'test/:id', component: TestComponent },
  {
    path: '',
    redirectTo: 'client',
    pathMatch: 'full'
  }
  // { path: '**', component: PageNotFoundComponent }
];

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    ClientComponent,
    SupervisorComponent,
    ReportComponent,
    IdFilterPipe,
    TestComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    FormsModule,
    ChartsModule,
    NgPipesModule,
    RouterModule.forRoot(appRoutes, { enableTracing: true }),
    ClarityModule.forRoot(),
    StoreModule.forRoot({
      availableDatasets: datasetReducer,
      supervisorConfiguration: supervisorReducer,
      currentTasks: taskReducer,
      selectedTask: selectTaskReducer,
      selectedReport: reportReducer,
      queryResult: queryTaskReducer
    }),
    AceEditorModule
  ],
  providers: [DatasetService, SupervisorService, TaskService, TestService],
  bootstrap: [AppComponent]
})
export class AppModule {}
