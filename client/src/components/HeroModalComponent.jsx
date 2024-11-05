import { useState, useEffect } from 'react';

import React from 'react'

const HeroModalComponent = () => {
    const [isModalOpen, setIsModalOpen] = useState(true);
    const closeModal = () => setIsModalOpen(false);
    return (
        <>
            {isModalOpen && (
                <div
                    id="extralarge-modal"
                    className="fixed top-0 left-0 right-0 z-50 w-full p-4 overflow-x-hidden overflow-y-auto md:inset-0 h-[calc(100%-1rem)] max-h-full bg-black bg-opacity-60 backdrop-blur-md flex items-center justify-center"
                >
                    <div className="relative w-full max-w-7xl max-h-full">
                        <div className="relative bg-white rounded-lg shadow">
                            <div className="flex items-center justify-between p-4 md:p-5 border-b rounded-t border-gray-200">
                                <h3 className="text-3xl font-bold text-black text-center w-full">
                                    Welcome to Engo 🚀
                                </h3>
                                <button
                                    type="button"
                                    onClick={closeModal} // Close modal
                                >
                                    <svg
                                        className="w-3 h-3"
                                        xmlns="http://www.w3.org/2000/svg"
                                        fill="none"
                                        viewBox="0 0 14 14"
                                    >
                                        <path
                                            stroke="currentColor"
                                            strokeLinecap="round"
                                            strokeLinejoin="round"
                                            strokeWidth="2"
                                            d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"
                                        />
                                    </svg>
                                    <span className="sr-only">Close modal</span>
                                </button>
                            </div>
                            <div className="p-4 md:p-5 space-y-4">
                                <p className="text-base leading-relaxed text-black">
                                    Engo is a custom Rule Engine built by Karthik Namboori (4th Year, CSE, PES University, Bangalore)
                                    for the Zeotap SDE Intern Assignment. To get started, click the
                                    <span className="font-bold font-sans"> Close </span> button and explore the rule engine!
                                </p>
                            </div>
                            <div className="flex items-center p-4 md:p-5 space-x-3 border-t border-gray-200 rounded-b">
                                <button
                                    onClick={closeModal}
                                    className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg px-5 py-2.5"
                                >
                                    Get Started
                                </button>
                                <button
                                    onClick={closeModal}
                                    className="bg-gray-800 text-white hover:bg-gray-700 border border-gray-600 rounded-lg px-5 py-2.5"
                                >
                                    Close
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </>
    )
}

export default HeroModalComponent