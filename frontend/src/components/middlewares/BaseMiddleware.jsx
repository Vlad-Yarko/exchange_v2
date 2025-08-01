import { Outlet } from 'react-router-dom'

import Header from '../elements/Header/Header'
import Footer from '../elements/Footer/Footer'

import { BaseContextProvider } from '../../context/BaseContext'


function BaseMiddleware() {
	return (
		<BaseContextProvider>
			<Header />
			<Outlet />
			<Footer />
		</BaseContextProvider>
	)
}


export default BaseMiddleware
