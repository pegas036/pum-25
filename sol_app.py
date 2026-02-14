# -*- coding: utf-8 -*-
"""
Created on Sat Feb 14 02:02:29 2026

@author: Piotr
"""

import streamlit as st
import pandas as pd
import pickle


def load_objects():
    with open("svr_model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("featurizer.pkl", "rb") as f:
        featurizer = pickle.load(f)
    return model, featurizer


model, featurizer = load_objects()

st.title('solubilty predictor app')

st.write('water solubility predicted by a pretrained SVM model, taking SMILES as input data (one or multiple)')


smiles_input = st.text_area('Enter SMILES (one per line):', height=150)

if st.button('predict solubility'):

    if smiles_input.strip() == '':
        st.warning("please enter input data")
    else:
        smiles_list = smiles_input.split("\n")
        clean_smiles = []
        for s in smiles_list:
            s = s.strip()           
            if s != "":             
                clean_smiles.append(s)

            smiles_list = clean_smiles

        try:
            X = featurizer.featurize(smiles_list)

            predictions = model.predict(X)

           
            results = pd.DataFrame({ 'SMILES': smiles_list,'predicted solubility': predictions })
               

            st.write('prediction results')
            st.dataframe(results)

        except Exception as e:
            st.error(f"Prediction failed: {e}")
