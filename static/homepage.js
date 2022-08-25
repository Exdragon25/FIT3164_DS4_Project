class CustomSelect {
    constructor(originalSelect) {
      this.originalSelect = originalSelect;
      this.customSelect = document.createElement("div");
      this.customSelect.classList.add("select");
  
      this.originalSelect.querySelectorAll("option").forEach((optionElement) => {
        const itemElement = document.createElement("div");
  
        itemElement.classList.add("select__item");
        itemElement.textContent = optionElement.textContent;
        this.customSelect.appendChild(itemElement);
  
        if (optionElement.selected) {
          this._select(itemElement);
        }
  
        itemElement.addEventListener("click", () => {
          if (
            this.originalSelect.multiple &&
            itemElement.classList.contains("select__item--selected")
          ) {
            this._deselect(itemElement);
          } else {
            this._select(itemElement);
          }
        });
      });
  
      this.originalSelect.insertAdjacentElement("afterend", this.customSelect);
      this.originalSelect.style.display = "none";
    }
  
    _select(itemElement) {
      const index = Array.from(this.customSelect.children).indexOf(itemElement);
  
      this.originalSelect.querySelectorAll("option")[index].selected = true;
      itemElement.classList.add("select__item--selected");
    }
  
    _deselect(itemElement) {
      const index = Array.from(this.customSelect.children).indexOf(itemElement);
  
      this.originalSelect.querySelectorAll("option")[index].selected = false;
      itemElement.classList.remove("select__item--selected");
    }
  }

  document.querySelectorAll(".custom-select").forEach((selectElement) => {
    new CustomSelect(selectElement);
  });

