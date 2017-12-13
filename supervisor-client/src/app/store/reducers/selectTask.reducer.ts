// Import task model, used for defining initial state
import { Task as State } from '../models/task.model';

// Import action declarations
import * as StoreActions from '../actions/store.actions';

export type Action = StoreActions.allSelectTaskActions;

// Define initial state
const initialState: State = {
  _id: '...',
  name: '...',
  description: '...',
  dataset: '...',
  type: '...',
  trained: false,
  best_training_accuracy: 0,
  best_training_model: '...',
  action: false,
  supervisor: false
};

// Reducer definition
export function reducer(state: State = initialState, action: Action) {
  switch (action.type) {
    case StoreActions.SELECT_TASK: {
      return action.payload;
    }

    default: {
      return state;
    }
  }
}
