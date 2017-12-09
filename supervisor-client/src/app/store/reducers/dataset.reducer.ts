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
		date_of_creation: null,
		features: null,
		rows: 0,
		active: false
	}
];

// Reducer definition
export function reducer(state: State[] = initialState, action: Action) {
	// console.log('User(Reducer) : ' + JSON.stringify(action.type));

	switch (action.type) {
		case StoreActions.SET_DATASET: {
			return state.map(set => {
				return set.name === action.payload.name ? Object.assign({}, set, action.payload) : set;
			});
			// console.log('User(Reducer) : User Login -> ' + JSON.stringify(action.payload));
			// return action.payload;
		}

		case StoreActions.GET_DATASETS: {
			console.log('User(Reducer) : User Logout');
			return [...state, action.payload];
		}

		default: {
			// console.log('User(Reducer) : Default Behavior!');
			return state;
		}
	}
}
