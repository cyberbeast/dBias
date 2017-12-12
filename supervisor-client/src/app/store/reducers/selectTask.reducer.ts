// Import task model, used for defining initial state
import { Task as State } from '../models/task.model';

// Import action declarations
import * as StoreActions from '../actions/store.actions';

export type Action = StoreActions.allSelectTaskActions;

// Reducer definition
export function reducer(state: State = null, action: Action) {
  switch (action.type) {
    case StoreActions.SELECT_TASK: {
      return action.payload;
    }

    default: {
      return state;
    }
  }
}
