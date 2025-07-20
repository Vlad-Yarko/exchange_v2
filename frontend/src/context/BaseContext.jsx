import { createContext } from 'react'


const BaseContext = createContext()


const BaseContextProvider = ({ children }) => {

	return (
		<BaseContext.Provider
			value={{

			}}
		>
			{children}
		</BaseContext.Provider>
	)
}


export { BaseContext, BaseContextProvider }
