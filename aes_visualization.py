#!/usr/bin/env python3
# AES-128 Encryption/Decryption Implementation
# Visualization helpers

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
from aes_utils import bytes_to_matrix, bytes_to_hex

def visualize_state_transformation(state_before, state_after, title, operation_name):
    """
    Visualize the transformation of a state matrix from before to after an operation.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    
    # Create heatmaps for before and after states
    im1 = ax1.imshow(state_before, cmap='Blues')
    im2 = ax2.imshow(state_after, cmap='Blues')
    
    # Add text annotations
    for i in range(4):
        for j in range(4):
            ax1.text(j, i, f"{state_before[i][j]:02X}", ha="center", va="center", color="black")
            ax2.text(j, i, f"{state_after[i][j]:02X}", ha="center", va="center", color="black")
    
    # Set titles and adjust layout
    ax1.set_title("Before " + operation_name)
    ax2.set_title("After " + operation_name)
    fig.suptitle(title, fontsize=16)
    
    # Hide axes ticks
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax2.set_xticks([])
    ax2.set_yticks([])
    
    # Add a colorbar
    fig.colorbar(im1, ax=[ax1, ax2], orientation='vertical', label='Byte Value')
    
    plt.tight_layout()
    plt.show()

def visualize_round_keys(round_keys):
    """
    Visualize all the round keys in a grid layout.
    """
    num_keys = len(round_keys)
    num_cols = 3  # Number of columns in the grid
    num_rows = (num_keys + num_cols - 1) // num_cols  # Ceiling division
    
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 5 * num_rows))
    axes = axes.flatten()  # Flatten to make indexing easier
    
    for i, key in enumerate(round_keys):
        if i < len(axes):
            im = axes[i].imshow(key, cmap='YlOrBr')
            
            # Add text annotations
            for r in range(4):
                for c in range(4):
                    axes[i].text(c, r, f"{key[r][c]:02X}", ha="center", va="center", color="black")
            
            axes[i].set_title(f"Round Key {i}")
            axes[i].set_xticks([])
            axes[i].set_yticks([])
            
            fig.colorbar(im, ax=axes[i])
    
    # Hide any unused subplots
    for i in range(num_keys, len(axes)):
        axes[i].axis('off')
    
    plt.tight_layout()
    plt.show()

def visualize_encryption_process(plaintext, key, encrypted_states, operation_names):
    """
    Visualize the entire encryption process with all state transformations.
    """
    num_states = len(encrypted_states)
    
    # Create a figure with multiple rows
    fig, axes = plt.subplots(num_states, 1, figsize=(8, 3 * num_states))
    
    # If there's only one state, axes won't be an array
    if num_states == 1:
        axes = [axes]
    
    for i, (state, op_name) in enumerate(zip(encrypted_states, operation_names)):
        im = axes[i].imshow(state, cmap='Blues')
        
        # Add text annotations
        for r in range(4):
            for c in range(4):
                axes[i].text(c, r, f"{state[r][c]:02X}", ha="center", va="center", color="black")
        
        axes[i].set_title(f"After {op_name}")
        axes[i].set_xticks([])
        axes[i].set_yticks([])
        
        fig.colorbar(im, ax=axes[i])
    
    plt.tight_layout()
    plt.show()

def generate_encryption_animation(plaintext, key, ciphertext):
    """
    Generate an animation showing the encryption process step by step.
    This is a placeholder - actual animation would require more complex code.
    """
    from aes_core import encrypt
    
    print("Animation placeholder: This would generate a step-by-step animation")
    print(f"Plaintext: {bytes_to_hex(plaintext)}")
    print(f"Key: {bytes_to_hex(key)}")
    
    # Encrypt with verbose=True to see the steps
    result = encrypt(plaintext, key, verbose=True)
    
    print(f"Ciphertext: {bytes_to_hex(result)}")
    print("An actual animation would require additional libraries like matplotlib animation or a GUI framework.")