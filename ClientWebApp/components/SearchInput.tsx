"use client";
import { useRouter } from "next/navigation";
import React, { useState, useEffect } from "react";

const apiSearch = "http://127.0.0.1:9999/search-product/";  // API endpoint

const SearchInput = () => {
  const [searchInput, setSearchInput] = useState<string>("");
  const [filteredSuggestions, setFilteredSuggestions] = useState<string[]>([]);
  const [isDropdownVisible, setDropdownVisible] = useState<boolean>(false);
  const router = useRouter();

  const [debounceTimeout, setDebounceTimeout] = useState<NodeJS.Timeout | null>(null);

  const searchProducts = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    router.push(`/search?search=${searchInput}`);
    setSearchInput("");
    setDropdownVisible(false);
  };

  const searchOnInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const searchValue = e.target.value;
    setSearchInput(searchValue);

    if (debounceTimeout) clearTimeout(debounceTimeout);

    const timeout = setTimeout(async () => {
      if (searchValue.trim().length > 0) {
        try {
          const res = await fetch(`${apiSearch}${searchValue.toLocaleLowerCase()}`);
          if (res.status === 200) {
            const matches = await res.json();
            console.log(matches);
            setFilteredSuggestions(matches.suggestions || []);
            setDropdownVisible(matches.suggestions?.length > 0);
          } else {
            console.error("Failed to fetch suggestions:", res.statusText);
            setFilteredSuggestions([]);
            setDropdownVisible(false);
          }
        } catch (error) {
          console.error("Error fetching suggestions:", error);
          setFilteredSuggestions([]);
          setDropdownVisible(false);
        }
      } else {
        setFilteredSuggestions([]);
        setDropdownVisible(false);
      }
    }, 300);

    setDebounceTimeout(timeout);
  };

  return (
    <form className="relative flex w-full justify-center" onSubmit={searchProducts}>
      {/* Input search */}
      <input
        type="text"
        value={searchInput}
        onChange={searchOnInput}
        placeholder="Type here"
        className="bg-gray-50 input input-bordered w-[70%] rounded-r-none outline-none focus:outline-none max-sm:w-full"
      />

      {/* Dropdown menu */}
      {isDropdownVisible && (
        <ul
          className="absolute z-10 bg-white border border-gray-300 w-[70%] max-sm:w-full rounded shadow-lg"
          style={{ top: "100%" }}
        >
          {filteredSuggestions.length > 0 ? (
            filteredSuggestions.map((item, index) => (
              <li
                key={index}
                onClick={() => {
                  setSearchInput(item);
                  setDropdownVisible(false);
                }}
                className="px-4 py-2 cursor-pointer hover:bg-gray-100"
              >
                {item}
              </li>
            ))
          ) : (
            <li className="px-4 py-2 text-gray-500">No results found</li>
          )}
        </ul>
      )}

      {/* Search button */}
      <button
        type="submit"
        className="btn bg-blue-500 text-white rounded-l-none rounded-r-xl hover:bg-blue-600"
      >
        Search
      </button>
    </form>
  );
};

export default SearchInput;