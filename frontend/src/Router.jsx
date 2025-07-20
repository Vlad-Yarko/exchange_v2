import {
	createRoutesFromElements,
	createBrowserRouter,
	Route,
} from 'react-router-dom'

import BaseMiddleware from './components/middlewares/BaseMiddleware'
import Home from './components/pages/Home/Home'


const router = createBrowserRouter(
	createRoutesFromElements(
		<Route path='/' element={<BaseMiddleware />}>
			<Route path='' element={<Home />}></Route>
		</Route>
	)
)


export default router
