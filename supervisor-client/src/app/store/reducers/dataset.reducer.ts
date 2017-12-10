// Import dataset model, used for defining initial state
import { Dataset as State } from '../models/dataset.model';

// Import action declarations
import * as StoreActions from '../actions/store.actions';

export type Action = StoreActions.allDatasetActions;

// Define initial state
const initialState: State[] = [
	{
		name: null,
		description: null,
		features: null,
		rows: 0,
		active: false
	}
];

// Reducer definition
export function reducer(state: State[] = initialState, action: Action) {
	switch (action.type) {
		case StoreActions.SET_DATASET: {
			return state.map(set => {
				return set.name === action.payload.name ? Object.assign({}, set, action.payload) : set;
			});
		}

		case StoreActions.GET_DATASETS: {
			return action.payload;
		}

		default: {
			return state;
		}
	}
}
