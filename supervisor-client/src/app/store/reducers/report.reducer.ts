// Import task model, used for defining initial state
import { Report as State } from '../models/report.model';

// Import action declarations
import * as StoreActions from '../actions/store.actions';

export type Action = StoreActions.allReportActions;

// Define initial state
const initialState: State = {
  _id: '...',
  model_details: [
    {
      accuracy: 0,
      classification_error: 0,
      confusion_matrix: [0, 0, 0, 0],
      feature_importance: [0],
      precision: 0,
      recall: 0,
      type: '...'
    }
  ],
  sv_visualizations: [],
  sv_distribution_by_salary: [],
  u_visualizations: [],
  sv_skewed: []
};

// Reducer definition
export function reducer(state: State = initialState, action: Action) {
  switch (action.type) {
    case StoreActions.SET_REPORT: {
      return action.payload;
    }

    default: {
      return state;
    }
  }
}
