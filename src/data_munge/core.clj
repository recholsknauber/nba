(ns data-munge.core)

;; (defn -main
;;   "I don't do a whole lot ... yet."
;;   [& args]
;;   (println "Hello, World!"))

(require '[clojure.data.csv :as csv]
	 '[clojure.java.io :as io])

(def whole-numbers (iterate inc 1))

;; Helper function to sort map keys by their order in a CSV.
(defn csv-data-sort-columns [csv-data coll]
  (let [coll-index (zipmap (map keyword (first csv-data)) whole-numbers)]
    (into (sorted-map-by #(compare (%1 coll-index) (%2 coll-index))) coll)))

;; Map data sort function over a sequence of maps.
(defn csv-data->sorted-maps [csv-data s]
  (map #(csv-data-sort-columns csv-data %1) s))


;; Convert CSV data to maps
(defn csv-data->maps [csv-data]
  (map zipmap
       (->> (first csv-data)
	    (map keyword)
	    repeat)
       (rest csv-data)))

;; Iterate a function over multiple keys
(defn update-keys [m ks f]
  (reduce #(update-in % [%2] f) m ks))

;; Use an smap of functions and keys to perform all necessary data munging.
(defn data_munging [coll funcs]
  (loop [m coll fks (clojure.set/select #(= (:order %) 1) funcs) counter 1 result []]
    (let [func (:function (first fks)) ks (:ks (first fks))]
      (cond
	(and (= counter 1) (= counter (count funcs))) ;; If only one data munge function, just return.
	(func m ks)
	(= counter 1) ;; If first data munge, conj initial map to result.
	(recur (func m ks)
	       (clojure.set/select #(= (:order %) (+ counter 1)) funcs)
	       (+ counter 1)
	       (conj result (func m ks)))
	(= counter (count funcs)) ;; If last data munge, return function on last result.
	(func (last result) ks)
	:else (recur (func (last result) ks) ;; Else, recur function on last result.
		     (clojure.set/select #(= (:order %) (+ counter 1)) funcs)
		     (+ counter 1)
		     (conj result (func (last result) ks)))))))
