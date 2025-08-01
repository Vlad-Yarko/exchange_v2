import {
	createRoutesFromElements,
	createBrowserRouter,
	Route,
} from 'react-router-dom'

import BaseMiddleware from './components/middlewares/BaseMiddleware'
import Home from './components/pages/Home/Home'
import Login from './components/pages/Login/Login'


const router = createBrowserRouter(
	createRoutesFromElements(
		<Route path='/' element={<BaseMiddleware />}>
			<Route path='' element={<Home />} />
			<Route path='auth/google' element={<Login />}/>
		</Route>
	)
)


export default router
