import { createSlice } from '@reduxjs/toolkit';
import type { PayloadAction } from "@reduxjs/toolkit";
import { IHomework } from "@/misc";

interface MiscState {
    isLaptop: boolean;
    hw: IHomework[];
}

const initialState: MiscState = {
    isLaptop: false,
    hw: []
};

export const miscSlice = createSlice({
    name: 'misc',
    initialState,
    reducers: {
        setData: (state, action: PayloadAction<object>) => {
            Object.assign(state, action.payload);
        },
        setIsLaptop: (state, action: PayloadAction<boolean>) => {
            state.isLaptop = action.payload;
        },
        editHW: (state, action: PayloadAction<any>) => {
            const found: IHomework | any = state.hw.find((h: IHomework) => h.subject === action.payload.subject);
            if (found) found.content[action.payload.contentNum] = action.payload.value;
        },
        addHWField: (state, action: PayloadAction<any>) => {
            const found: IHomework | any = state.hw.find((h: IHomework) => h.subject === action.payload);
            if (found) found.content.push('');
        },
        removeHWField: (state, action: PayloadAction<any>) => {
            const found: IHomework | any = state.hw.find((h: IHomework) => h.subject === action.payload[0]);
            if (found) found.content.splice(action.payload[1], 1);
        },
        deletePhoto: (state, action: PayloadAction<any>) => {
            // @ts-ignore
            state.hw[action.payload].image = null;
        }
    }
})

export const { setData, setIsLaptop, editHW, addHWField, removeHWField, deletePhoto } = miscSlice.actions;
export default miscSlice.reducer;