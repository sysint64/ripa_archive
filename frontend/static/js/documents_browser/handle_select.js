function handleSelect($this, event) {
    if (event.ctrlKey) {
        $this.toggleClass("selected");
    } else if (event.shiftKey) {
        if ($lastSelected == null) {
            $selectable.removeClass("selected");
            $this.addClass("selected");
        } else {
            var $firstElement, $lastElement;

            if ($lastSelected.isBefore($this)) {
                $firstElement = $lastSelected;
                $lastElement = $this;
            } else {
                $firstElement = $this;
                $lastElement = $lastSelected;
            }

            $firstElement.nextUntil($lastElement).addBack().add($lastElement).addClass("selected");
            $this.addClass("selected");
        }
    } else {
        $selectable.removeClass("selected");
        $this.addClass("selected");
    }

    if ($this.hasClass("selected")) {
        $lastSelected = $this;
    } else {
        $selectable.removeClass("selected");
        $lastSelected = null;
    }

    if (onSelectChange != null)
        onSelectChange();
}
