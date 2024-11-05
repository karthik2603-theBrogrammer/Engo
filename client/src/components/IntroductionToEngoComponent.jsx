import React from 'react'
import { introductionComponents } from '../../utils'

const IntroductionToEngoComponent = () => {
    return (
        <div className='w-full flex items-center justify-center flex-col mt-9'>
            <div className="flex flex-col items-center justify-center -gap-3">
                <h1 className='text-[30px] text-center'>A Quick Introduction to Engo!</h1>
                <p>{"(Reload the application to view this again!)"}</p>
            </div>
            <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3'>
                {
                    introductionComponents?.map((introductionComponent, key) => (
                        <div key={key} className="m-4 p-4 bg-slate-300 rounded-lg" >
                            <p className='text-[20px] md:text-[22px] font-bold'>{introductionComponent?.title}</p>
                            <p className='text-sm'>
                                {introductionComponent?.description}
                                {introductionComponent?.url && (
                                    <>
                                        {' '}
                                        <a
                                            href={introductionComponent.url}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                            className="text-blue-500 hover:underline"
                                        >
                                            Know more here.
                                        </a>
                                    </>
                                )}
                            </p>
                        </div>
                    ))
                }
            </div>
        </div>
    )
}

export default IntroductionToEngoComponent
